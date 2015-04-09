import java.io.IOException;
import java.util.ArrayList;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

public class SecondMR_Volatility {

    public static class Map2 extends Mapper<Object, Text, Text, Text> {

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            try {
                // Split the received value using "\t"
                String[] volatilityValues = value.toString().split("\t");
                context.write(new Text(volatilityValues[0]), new Text(volatilityValues[1])); //write the file name and volatility values of each month
            }
            catch (Exception e){
            }
        }
    }

    public static class Reduce2 extends Reducer<Text, Text, Text, Text> {

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
            double sum=0.0;

            //Find the difference between xI and average of the value
            for (int i=0; i<xiValues.size(); i++){
                double xminxbar = Double.parseDouble(xiValues.get(i).toString())-xBar;
                sum+=Math.pow(xminxbar,2)/xiValues.size();
            }
            //Final Volitility calculated using formula
            double vol = Math.sqrt(sum);
            context.write(key, new Text(Double.toString(vol)));
        }
    }
}