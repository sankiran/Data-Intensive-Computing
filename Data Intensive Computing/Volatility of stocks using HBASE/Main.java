
import java.util.Map;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

public class Main{


	public static void main(String[] args){

		Configuration conf = HBaseConfiguration.create();
		try {
			
			HBaseAdmin admin = new HBaseAdmin(conf);
			HTableDescriptor tableDescriptor = new HTableDescriptor(TableName.valueOf("raw"));
			tableDescriptor.addFamily(new HColumnDescriptor("stock"));
			tableDescriptor.addFamily(new HColumnDescriptor("time"));
			tableDescriptor.addFamily(new HColumnDescriptor("price"));
			if ( admin.isTableAvailable("raw")){
				admin.disableTable("raw");
				admin.deleteTable("raw");
			}
			admin.createTable(tableDescriptor);


			Job job = Job.getInstance();
			job.setJarByClass(Main.class);
			FileInputFormat.addInputPath(job, new Path(args[0]));
			job.setInputFormatClass(TextInputFormat.class);
			job.setMapperClass(Job1.Map.class);
			TableMapReduceUtil.initTableReducerJob("raw", null, job);
			job.setNumReduceTasks(0);
			job.waitForCompletion(true);
			
			//Starting new job for first mapreduce.
			HTableDescriptor tableDescriptor1 = new HTableDescriptor(TableName.valueOf("FirstMapper"));
			tableDescriptor1.addFamily(new HColumnDescriptor("Adj_Close_Val"));
			if ( admin.isTableAvailable("FirstMapper")){
				admin.disableTable("FirstMapper");
				admin.deleteTable("FirstMapper");
			}
			admin.createTable(tableDescriptor1);
			
			Scan scan = new Scan();
			scan.setCaching(500);    
			scan.setCacheBlocks(false);
			
			Job job1 = Job.getInstance();
			job1.setJarByClass(FirstMR_Volatility.class);
			TableMapReduceUtil.initTableMapperJob(
					  "raw",      
					  scan,             
					  FirstMR_Volatility.Map1.class,   
					  Text.class,             
					  Text.class,             
					  job1);
			TableMapReduceUtil.initTableReducerJob(
					  "FirstMapper",        
					  FirstMR_Volatility.Reduce1.class,
					  job1);
			job1.setNumReduceTasks(1);
			job1.waitForCompletion(true);
			
			
			//Starting job for MapReduce 2
			HTableDescriptor tableDescriptor2 = new HTableDescriptor(TableName.valueOf("SecondMapper"));
			tableDescriptor2.addFamily(new HColumnDescriptor("Vol_Vals"));
			if ( admin.isTableAvailable("SecondMapper")){
				admin.disableTable("SecondMapper");
				admin.deleteTable("SecondMapper");
			}
			admin.createTable(tableDescriptor2);
			
			Scan scan1 = new Scan();
			scan1.setCaching(500);    
			scan1.setCacheBlocks(false);
			
			Job job2 = Job.getInstance();
			job2.setJarByClass(SecondMR_Volatility.class);
			TableMapReduceUtil.initTableMapperJob(
					  "FirstMapper",      
					  scan1,             
					  SecondMR_Volatility.Map2.class,   
					  Text.class,             
					  Text.class,             
					  job2);
			TableMapReduceUtil.initTableReducerJob(
					  "SecondMapper",        
					  SecondMR_Volatility.Reduce2.class,
					  job2);
			job2.setNumReduceTasks(1);
			job2.waitForCompletion(true);
			
			//Starting job for MapReduce 3
			HTableDescriptor tableDescriptor3 = new HTableDescriptor(TableName.valueOf("ThirdMapper"));
			tableDescriptor3.addFamily(new HColumnDescriptor("Fin_Val"));
			tableDescriptor3.addFamily(new HColumnDescriptor("Fin_Comp_Name"));
			if ( admin.isTableAvailable("ThirdMapper")){
				admin.disableTable("ThirdMapper");
				admin.deleteTable("ThirdMapper");
			}
			admin.createTable(tableDescriptor3);
			
			Scan scan2 = new Scan();
			scan2.setCaching(500);    
			scan2.setCacheBlocks(false);
			
			Job job3 = Job.getInstance();
			job3.setJarByClass(FinalMR_Volatility.class);
			TableMapReduceUtil.initTableMapperJob(
					  "SecondMapper",      
					  scan2,             
					  FinalMR_Volatility.Map3.class,   
					  Text.class,             
					  Text.class,             
					  job3);
			TableMapReduceUtil.initTableReducerJob(
					  "ThirdMapper",        
					  FinalMR_Volatility.Reduce3.class,
					  job3);
			job3.setNumReduceTasks(1);
			job3.waitForCompletion(true);
			
			//Writing to the console by printing
			HTable table = new HTable(conf,"ThirdMapper");
			Scan scan5 = new Scan();
			TreeMap<Double, String> map = new TreeMap<Double, String>();
			ResultScanner scanner = table.getScanner(scan5);
			for(Result scannerResult:scanner) { 
				String companyName=new String(scannerResult.getValue(Bytes.toBytes("Fin_Comp_Name"), Bytes.toBytes("Fin_Comp_Name_Attr")));
				String vola_val=new String(scannerResult.getValue(Bytes.toBytes("Fin_Val"), Bytes.toBytes("Fin_Val_Attr")));
				System.out.println(companyName+" :: " +vola_val ); map.put(Double.valueOf(vola_val), companyName);
				} 
				System.out.println("Top 10 Stocks having Lowest Volatility are: ");
				int count = 1;
				for(Map.Entry<Double, String> entry : map.entrySet()) {
					Double key = entry.getKey();
					String value = entry.getValue();
					System.out.println(value+" "+ key);
					if(count == 10) System.out.println("Top 10 Stocks having Highest Volatility are:");
					count++; }
			admin.close();
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
}

