import java.io.IOException;
import java.util.*;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class FirstMR_Volatility {
	
	public static class Map1 extends TableMapper<Text, Text> {
		public static final byte[] STOCK_NAME = "stock".getBytes();
		public static final byte[] STOCK_NAME_ATTR = "name".getBytes();
		public static final byte[] DATE = "time".getBytes();
		public static final byte[] DATE_ATTR1 = "yr".getBytes();
		public static final byte[] DATE_ATTR2 = "mm".getBytes();
		public static final byte[] DATE_ATTR3 = "dd".getBytes();
		public static final byte[] STOCK_PRICE = "price".getBytes();
		//public static final byte[] STOCK_PRICE_ATTR = "price".getBytes();

        public void map(ImmutableBytesWritable row, Result value, Context context) throws IOException, InterruptedException {

            try {
            //String[] line = value.toString().split(","); //split every line wrt "," in csv file
            //if(!line[0].equalsIgnoreCase("Date")) {// ignore the first row which has labels

                //get filename which is to be read
                String fileName = new String(value.getValue(STOCK_NAME, STOCK_NAME_ATTR));

                //get the date of every row
                //String[] splitDate = line[0].split("-");

                //get the day value from the date
                String year = new String(value.getValue(DATE, DATE_ATTR1));

                //get the month value from the date
                String month = new String(value.getValue(DATE, DATE_ATTR2));

                //append the filename, year and month to single string value
                String file_month_year = fileName + "::" + year + "::" + month;

                //get the day and its corresponding adjacent close value,separated by "::" delimiter
                String day = new String(value.getValue(DATE, DATE_ATTR3));
                String adjClose = new String(value.getValue(STOCK_PRICE, STOCK_PRICE));
                String day_adjClose = day + "::" + adjClose;
                //System.out.println(file_month_year + "-"+ day_adjClose);
                context.write(new Text(file_month_year), new Text(day_adjClose));
                //}
            }
                catch (Exception e) {// catch any exceptions, if any
                e.printStackTrace();
                }
        }
	}

	public static class Reduce1 extends TableReducer<Text, Text, ImmutableBytesWritable> {
		
		public static final byte[] ADJ_CLS = "Adj_Close_Val".getBytes();
		  public static final byte[] ADJ_CLS_ATTR = "AdjCls_Attr".getBytes();

        public void reduce(Text key, Iterable<Text> values,Context context) throws IOException, InterruptedException {

            //split the key using "::" delimiter
            String fileVal = key.toString();

            //remove the csv label from the file name
            //String fileVal=file_MonthYear[0].split(".csv")[0];

            //create the list to add every value passed from the map
            List <String> daysAdjValsList = new ArrayList<String>();

            for (Text val:values) {
                //add each value to the array list
                daysAdjValsList.add(val.toString());
            }

            //sort the list
            Collections.sort(daysAdjValsList);

            //find the size of the array list
            int len = daysAdjValsList.size();

            //find the first day in the list and get its adjacent close value
            String beginDayVals = daysAdjValsList.get(0);
            String[] day_AdjCloseSplitBegin = beginDayVals.toString().split("::");
            int dayValuesInIntBegin = Integer.parseInt(day_AdjCloseSplitBegin[0]);
            double adjValuesInIntBegin = Double.parseDouble(day_AdjCloseSplitBegin[1]);

            //find the last day in the list and get its adjacent close value
            String closeDayVals = daysAdjValsList.get(len-1);
            String[] day_AdjCloseSplitEnd = closeDayVals.toString().split("::");
            int dayValuesInIntClose = Integer.parseInt(day_AdjCloseSplitEnd[0]);
            double adjValuesInIntClose = Double.parseDouble(day_AdjCloseSplitEnd[1]);

            //find the difference in the adjacent close value of first and last day
            double diffInVolatility = adjValuesInIntClose-adjValuesInIntBegin;
            double valueAdj_Diff = diffInVolatility/adjValuesInIntBegin;
            String valueAdj = String.valueOf(valueAdj_Diff);

            //write the filename as key and Adjacent difference as value
            //context.write(new Text(fileVal), new Text(valueAdj));
            Put put = new Put(Bytes.toBytes(fileVal));
            put.add(ADJ_CLS, ADJ_CLS_ATTR, Bytes.toBytes(Double.toString(valueAdj_Diff)));
            //System.out.println(fileVal + "-" + valueAdj_Diff);
            context.write(null, put);
        }
    }
}
