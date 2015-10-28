package org.apache.accumulo.examples.simple.mapreduce;

import java.io.IOException;
import java.io.PrintStream;
import org.apache.accumulo.core.client.mapreduce.AccumuloOutputFormat;
import org.apache.accumulo.core.data.Mutation;
import org.apache.accumulo.core.data.Value;
import org.apache.accumulo.core.security.ColumnVisibility;
import org.apache.accumulo.core.util.CachedConfiguration;
import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.Parser;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class WordCount
extends Configured
implements Tool
{
    private static Options opts;
    private static Option passwordOpt;
    private static Option usernameOpt;
    private static String USAGE = "wordCount <instance name> <zoo keepers> <input dir> <output table>";
    
    static
    {
        usernameOpt = new Option("u", "username", true, "username");
        passwordOpt = new Option("p", "password", true, "password");
        
        opts = new Options();
        
        opts.addOption(usernameOpt);
        opts.addOption(passwordOpt);
    }
    
    public static class MapClass
    extends Mapper<LongWritable, Text, Text, Mutation>
    {
        public void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, Mutation>.Context output)
        throws IOException
        {
            FileSplit fileSplit = (FileSplit)output.getInputSplit();
            String fn = fileSplit.getPath().getName();
            
            String[] words = value.toString().split("\\s+");
            String[] arrayOfString1;
            int j = (arrayOfString1 = words).length;
            for (int i = 0; i < j; i++)
            {
                String word = arrayOfString1[i];
                if (word.equalsIgnoreCase("win"))
                {
                    if (fn.contains("east_"))
                    {
                        Mutation mutation = new Mutation(new Text(fn.substring(4, fn.length() - 4)));
                        mutation.put(new Text("->EAST"), new Text("wins"), new ColumnVisibility("east"), new Value("1".getBytes()));
                        try
                        {
                            output.write(new Text("Win"), mutation);
                        }
                        catch (InterruptedException e)
                        {
                            e.printStackTrace();
                        }
                    }
                    else if (fn.contains("west_"))
                    {
                        Mutation mutation = new Mutation(new Text(fn.substring(4, fn.length() - 4)));
                        mutation.put(new Text("->WEST"), new Text("wins"), new ColumnVisibility("west"), new Value("1".getBytes()));
                        try
                        {
                            output.write(new Text("Win"), mutation);
                        }
                        catch (InterruptedException e)
                        {
                            e.printStackTrace();
                        }
                    }
                }
                else if (word.equalsIgnoreCase("lose")) {
                    if (fn.contains("east_"))
                    {
                        Mutation mutation = new Mutation(new Text(fn.substring(4, fn.length() - 4)));
                        mutation.put(new Text("->EAST"), new Text("losses"), new ColumnVisibility("east"), new Value("1".getBytes()));
                        try
                        {
                            output.write(new Text("Lose"), mutation);
                        }
                        catch (InterruptedException e)
                        {
                            e.printStackTrace();
                        }
                    }
                    else if (fn.contains("west_"))
                    {
                        Mutation mutation = new Mutation(new Text(fn.substring(4, fn.length() - 4)));
                        mutation.put(new Text("->WEST"), new Text("losses"), new ColumnVisibility("west"), new Value("1".getBytes()));
                        try
                        {
                            output.write(new Text("Lose"), mutation);
                        }
                        catch (InterruptedException e)
                        {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }
    }
    
    public int run(String[] unprocessed_args)
    throws Exception
    {
        Parser p = new BasicParser();
        
        CommandLine cl = p.parse(opts, unprocessed_args);
        String[] args = cl.getArgs();
        
        String username = cl.getOptionValue(usernameOpt.getOpt(), "root");
        String password = cl.getOptionValue(passwordOpt.getOpt(), "secret");
        if (args.length != 4)
        {
            System.out.println("ERROR: Wrong number of parameters: " + args.length + " instead of 4.");
            return printUsage();
        }
        Job job = new Job(getConf(), WordCount.class.getName());
        job.setJarByClass(getClass());
        
        job.setInputFormatClass(TextInputFormat.class);
        TextInputFormat.setInputPaths(job, new Path[] { new Path(args[2]) });
        
        job.setMapperClass(MapClass.class);
        
        job.setNumReduceTasks(0);
        
        job.setOutputFormatClass(AccumuloOutputFormat.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Mutation.class);
        AccumuloOutputFormat.setOutputInfo(job.getConfiguration(), username, password.getBytes(), true, args[3]);
        AccumuloOutputFormat.setZooKeeperInstance(job.getConfiguration(), args[0], args[1]);
        job.waitForCompletion(true);
        return 0;
    }
    
    private int printUsage()
    {
        HelpFormatter hf = new HelpFormatter();
        hf.printHelp(USAGE, opts);
        return 0;
    }
    
    public static void main(String[] args)
    throws Exception
    {
        int res = ToolRunner.run(CachedConfiguration.getInstance(), new WordCount(), args);
        System.exit(res);
    }
}
