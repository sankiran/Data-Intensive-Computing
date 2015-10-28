import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import java.util.Collections;

public class FinalMR_Volatility {

    public static class Map3 extends Mapper<Object, Text, Text, Text> {

        public void map(Object keys, Text value, Context context) throws IOException, InterruptedException {
            String[] line = value.toString().split("\t");
            String companyName = line[0];
            String adjacentValue = line[1];

            try{
                context.write(new Text("Company_Volatility:"),new Text(adjacentValue+"::"+companyName));
            }
            catch(Exception e){
                e.printStackTrace();
            }
        }
    }

    public static class Reduce3 extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
            int countValue=0;
            List <String> listValues = new ArrayList<String>();

            for (Text val: values){
                listValues.add(val.toString());
            }
            Collections.sort(listValues);

            for(String obj : listValues){
                countValue++;
                if(countValue <= 10) {
                    context.write(new Text(key.toString()), new Text(obj.toString()));
                }
                if(countValue>(listValues.size()-10)) {
                    context.write(new Text(key.toString()), new Text(obj.toString()));
                }

            }
        }


    }


}
