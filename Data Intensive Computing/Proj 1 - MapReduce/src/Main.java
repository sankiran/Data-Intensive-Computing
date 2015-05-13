
import java.util.Date;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Main {

    public static void main(String[] args) throws Exception {
        long start = new Date().getTime();
        Configuration conf = new Configuration();

        Job job = Job.getInstance();
        job.setJarByClass(FirstMR_Volatility.class);
        Job job2 = Job.getInstance();
        job2.setJarByClass(SecondMR_Volatility.class);
        Job job3 = Job.getInstance();
        job3.setJarByClass(FinalMR_Volatility.class);


        job.setJarByClass(FirstMR_Volatility.class);
        job.setMapperClass(FirstMR_Volatility.Map1.class);
        job.setReducerClass(FirstMR_Volatility.Reduce1.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);


        job2.setJarByClass(SecondMR_Volatility.class);
        job2.setMapperClass(SecondMR_Volatility.Map2.class);
        job2.setReducerClass(SecondMR_Volatility.Reduce2.class);

        job2.setMapOutputKeyClass(Text.class);
        job2.setMapOutputValueClass(Text.class);

        job3.setJarByClass(FinalMR_Volatility.class);
        job3.setMapperClass(FinalMR_Volatility.Map3.class);
        job3.setReducerClass(FinalMR_Volatility.Reduce3.class);

        job3.setMapOutputKeyClass(Text.class);
        job3.setMapOutputValueClass(Text.class);


        FileInputFormat.addInputPath(job, new Path(args[0]));

        FileOutputFormat.setOutputPath(job, new Path("Inter_"+args[1]));
        FileInputFormat.addInputPath(job2, new Path("Inter_" + args[1]));
        FileOutputFormat.setOutputPath(job2, new Path("Output_" + args[1]));
        FileInputFormat.addInputPath(job3, new Path("Output_" + args[1]));
        FileOutputFormat.setOutputPath(job3, new Path("Final_" + args[1]));
        ;
        job.waitForCompletion(true);
        boolean status = job2.waitForCompletion(true);
        status = job3.waitForCompletion(true);
        if (status == true) {
            long end = new Date().getTime();
            System.out.println("\nJob took " + (end-start)/1000 + "seconds\n");
        }
    }
}
