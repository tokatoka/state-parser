use std::{fs::{File, self}, io::Read, path::{PathBuf, Path}};
use core::time::Duration;
use libafl::{inputs::{BytesInput, Input}, state::StdStateDump};
use structopt::StructOpt;

#[derive(Debug, StructOpt)]
struct Opt {
    #[structopt(short = "e")]
    execs: bool,

    #[structopt(short = "t")]
    time: u64,

    #[structopt(short = "w", parse(from_os_str))]
    workdir: PathBuf,

    #[structopt(short = "s", parse(from_os_str))]
    dumpsdir: PathBuf,
}

fn execs_mode(dumps: &Vec<StdStateDump<BytesInput>>) -> Result<(), Box<dyn std::error::Error>> {
    let mut execs = 0;
    for dump in dumps {
        execs += dump.executions;
        println!("execs: {}", dump.executions)
    }
    println!("{execs}");
    Ok(())
}

fn testcase_mode(dumps: &Vec<StdStateDump<BytesInput>>, workdir: &PathBuf, frame: Duration) -> Result<(), Box<dyn std::error::Error>> {
    // Get when the first guy started
    let mut earliest = dumps[0].start_time;
    for dump in dumps {
        if dump.start_time < earliest {
            earliest = dump.start_time;
        }
    }

    let mut ctr = 0;
    // Now iterate over every thing and write stuff to workdir 
    for dump in dumps {
        for testcase in &dump.testcases {
            let do_write = testcase.timestamp - earliest < frame;
            if do_write {
                let write_path = workdir.join(Path::new(&ctr.to_string()));
                let _  = testcase.input.to_file(write_path);
                
                ctr += 1;
            }
        }
    }
    println!("Written {ctr} testcases!");

    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let opt = Opt::from_args();

    let workdir = PathBuf::from(opt.workdir);
    let mut dumps= vec![];
    let frame = Duration::from_secs(opt.time);
    for entry in fs::read_dir(opt.dumpsdir.clone())? {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            for dump_entry in fs::read_dir(path)? {
                let dump_entry = dump_entry?;
                let dump = dump_entry.path();
                let mut file = File::open(&dump)?;
                let mut contents = Vec::new();
                file.read_to_end(&mut contents)?;
                let this_data: StdStateDump<BytesInput> = postcard::from_bytes(&contents)?;
                dumps.push(this_data);
                println!("Read {:#?}", dump);
            }
        }
    }

    if dumps.len() < 1 {
        eprintln!("No dumps found!");
        std::process::exit(0);
    }

    if opt.execs {
        execs_mode(&dumps)
    }
    else {
        testcase_mode(&dumps, &workdir, frame)
    }


}
