import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

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

import java.util.Collections;

public class FinalMR_Volatility {

    public static class Map3 extends TableMapper<Text, Text> {
    	public static final byte[] FIN_VALS = "Vol_Vals".getBytes();
    	public static final byte[] FIN_VALS_ATTR = "Vol_Vals_Attr".getBytes();

        public void map(ImmutableBytesWritable row, Result value, Context context) throws IOException, InterruptedException {
            //String line = new String(value.getValue(FIN_VALS, FIN_VALS_ATTR));
            String companyName = new String(row.get());
            String volFinValue = new String(value.getValue(FIN_VALS, FIN_VALS_ATTR));

            try{
                context.write(new Text("Company_Volatility:"),new Text(volFinValue+"::"+companyName));
            }
            catch(Exception e){
                e.printStackTrace();
            }
        }
    }

    public static class Reduce3 extends TableReducer<Text, Text, ImmutableBytesWritable> {
    	public static final byte[] THIRD_MP_VALS = "Fin_Val".getBytes();
    	public static final byte[] THIRD_MP_CMP_NAME = "Fin_Comp_Name".getBytes();
    	public static final byte[] THIRD_MP_VALS_ATTR = "Fin_Val_Attr".getBytes();
    	public static final byte[] THIRD_MP_CMP_ATTR = "Fin_Comp_Name_Attr".getBytes();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
            int i;
        	int countValue=0;
            List <String> listValues = new ArrayList<String>();

            for (Text val: values){
                listValues.add(val.toString());
            }
            Collections.sort(listValues);

            for(String obj : listValues){
                countValue++;
                //String cnt = Integer.toString(countValue);
                if(countValue <= 10) {
                	Put put = new Put(Bytes.toBytes(obj.split("::")[1]));
                    put.add(THIRD_MP_VALS, THIRD_MP_VALS_ATTR, Bytes.toBytes(obj.split("::")[0]));
                    put.add(THIRD_MP_CMP_NAME, THIRD_MP_CMP_ATTR, Bytes.toBytes(obj.split("::")[1]));
                    System.out.println(put);
                    context.write(null, put);
                    //context.write(new Text(key.toString()), new Text(obj.toString()));
                }
                if(countValue>(listValues.size()-10)) {
                	Put put = new Put(Bytes.toBytes(obj.split("::")[1]));
                	put.add(THIRD_MP_VALS, THIRD_MP_VALS_ATTR, Bytes.toBytes(obj.split("::")[0]));
                	put.add(THIRD_MP_CMP_NAME, THIRD_MP_CMP_ATTR, Bytes.toBytes(obj.split("::")[1]));
                	System.out.println(put);
                    context.write(null, put);
                    //context.write(new Text(key.toString()), new Text(obj.toString()));
                }

            }
        }


    }


}
