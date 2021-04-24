use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::fs;
use std::fs::File;
use std::io::Write;
use std::io::Read;
use std::str;
use std::io::LineWriter;

fn rand_xor(mut input : &[u8], mut rng : StdRng) -> String {
    return input
        .into_iter()
        .map(|c| format!("{:02x}", (c ^ rng.gen::<u8>())))
        .collect::<Vec<String>>()
        .join("");
}

fn main() -> std::io::Result<()> {
    for seed in 1618016400..1618707600{
        //println!("time: {}", seed);
        let mut seeded = StdRng::seed_from_u64(seed);
        let mut f  = File::open("../out2.txt")?;
        let mut flag = [0;41];
        f.read(&mut flag)?;
        let xored = rand_xor(&mut flag,seeded);
        println!("{}", xored);
    }
    Ok(())
}
