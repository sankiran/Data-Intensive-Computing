/* sankiran_pig.pig */
load_data = LOAD 'hdfs:///pigdata' using PigStorage(',','-tagFile');
req_data = FOREACH load_data GENERATE $0 as StockName, $1 as Date, $7 as Adjusted_Close;
rem_fline = FILTER req_data by (Date != 'Date');
yr_month =  FOREACH rem_fline GENERATE StockName as StockName, SUBSTRING(Date,0,7) AS ym, SUBSTRING(Date,8,10) AS day, Adjusted_Close as adj_cls;
values_group = GROUP yr_month BY (StockName,ym);
FirstLastVal = FOREACH values_group GENERATE FLATTEN(yr_month.(StockName,ym,day,adj_cls)), MIN(yr_month.day) AS fday, MAX(yr_month.day) AS lday;
req_vals = FILTER FirstLastVal BY (fday==day OR lday==day);

rv_filter = FOREACH req_vals GENERATE StockName AS leftstock, ym AS l_ym,day AS leftday, adj_cls AS lt_adj_close;
rv_filter2 = FOREACH req_vals GENERATE StockName AS rtstock, ym AS r_ym,day AS rtday, adj_cls AS rt_adj_close;

A = JOIN rv_filter BY (l_ym), rv_filter2 BY (r_ym);
B = FILTER A BY ((leftday < rtday) AND (leftstock == rtstock)) ;
C = FOREACH B GENERATE leftstock AS StockNames, l_ym AS yr_mon, ((rt_adj_close - lt_adj_close) / lt_adj_close) AS x;
D = GROUP C BY StockNames;
E = FOREACH D GENERATE FLATTEN(C.StockNames) AS StockNameList, AVG(C.x) as meanx , COUNT(C.x) AS cnt;
F = DISTINCT E;
G = JOIN C BY StockNames, F BY StockNameList;
H = FOREACH G GENERATE StockNames, x, meanx, cnt;
I = FOREACH H GENERATE StockNames, ((x - meanx) * (x - meanx)) AS xfin, cnt;
J = GROUP I BY StockNames;
K = FOREACH J GENERATE FLATTEN(I.StockNames) AS Stocks, SUM(I.xfin) AS xval, FLATTEN(I.cnt) AS count;
L = DISTINCT K;
M = FOREACH L GENERATE Stocks, SQRT(xval / ( count - 1 )) AS vol_val ;
N = FILTER M BY vol_val is not null AND vol_val != 0.0;
O = ORDER N BY vol_val asc;
P = ORDER N BY vol_val desc;
Q = LIMIT O 10 ;
R = LIMIT P 10 ;
S = UNION Q,R;
STORE S INTO 'hdfs:///pigdata/hw3_out'; 
