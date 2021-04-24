use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::fs::File;
use std::io::Write;
use std::io::Read;

fn get_rng() -> StdRng {
    let seed = 13371337;
    return StdRng::seed_from_u64(seed);
}

fn rand_xor(mut buff : &[u8]) -> String {
    let mut rng = get_rng();
    return buff
        .into_iter()
        .map(|c| format!("{:02x}", (c ^ rng.gen::<u8>())))
        .collect::<Vec<String>>()
        .join("");
}

fn main() -> std::io::Result<()> {
    let mut f = File::open("out.txt")?;
    let mut buf = [0;58]; 
    f.read(&mut buf)?;
    println!("{:?}", &buf[..]);
    let xored = rand_xor(&mut buf);
    println!("{}", xored);
    let mut file = File::create("out.txt")?;
    file.write(xored.as_bytes())?;
    Ok(())
}
