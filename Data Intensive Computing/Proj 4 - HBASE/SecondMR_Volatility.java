import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;

public class SecondMR_Volatility {

    public static class Map2 extends TableMapper<Text, Text> {
    	public static final byte[] ROR_VALUES = "Adj_Close_Val".getBytes();
    	public static final byte[] ROR_VALUES_ATTR = "AdjCls_Attr".getBytes();
		
        public void map(ImmutableBytesWritable row, Result value, Context context) throws IOException, InterruptedException {
            try {
                // Split the received value using "\t"
                String volatilityValues = new String(value.getValue(ROR_VALUES, ROR_VALUES_ATTR));
                String key_val = new String(row.get()).split("\t")[0];
                String key_new = key_val.split("::")[0];
                //System.out.println(key_new+ volatilityValues);
                context.write(new Text(key_new), new Text(volatilityValues)); //write the file name and volatility values of each month
            }
            catch (Exception e){
            }
        }
    }

    public static class Reduce2 extends TableReducer<Text, Text, ImmutableBytesWritable> {
    	
    	public static final byte[] VOL_VALS = "Vol_Vals".getBytes();
    	public static final byte[] VOL_VALS_ATTR = "Vol_Vals_Attr".getBytes();

        public void reduce(Text key, Iterable<Text> values,Context context) throws IOException, InterruptedException {

            ArrayList <String> xiValues = new ArrayList<String>();
            double sumOfXiValues = 0.0;

            for (Text value:values) {
                //Find the summation of xI values for all 36 months
                xiValues.add(value.toString());
                sumOfXiValues += Double.parseDouble(value.toString());
            }
            // Find the average of the xI values over 36 months.
            double xBar = sumOfXiValues/xiValues.size();
            //System.out.println("xbar"+xBar);
            double sum=0.0;

            //Find the difference between xI and average of the value
            for (int i=0; i<xiValues.size(); i++){
                double xminxbar = Double.parseDouble(xiValues.get(i).toString())-xBar;
                //System.out.println("xminxbar" +xminxbar);
                sum+=Math.pow(xminxbar,2)/(xiValues.size()-1);
            }
            //Final Volitility calculated using formula
            double vol = Math.sqrt(sum);
            if(xiValues.size() > 1 && vol!= 0) {
            Put put = new Put(Bytes.toBytes(key.toString()));
            put.add(VOL_VALS, VOL_VALS_ATTR, Bytes.toBytes(Double.toString(vol)));
            //System.out.println(key.toString()+" :: "+vol);
            context.write(null, put);
            }
            //context.write(key, new Text(Double.toString(vol)));
        }
    }
}