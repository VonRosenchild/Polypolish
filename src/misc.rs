// Copyright 2021 Ryan Wick (rrwick@gmail.com)
// https://github.com/rrwick/Polypolish

//This file is part of Polypolish. Polypolish is free software: you can redistribute it and/or
// modify it under the terms of the GNU General Public License as published by the Free Software
// Foundation, either version 3 of the License, or (at your option) any later version. Polypolish
// is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
// implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
// Public License for more details. You should have received a copy of the GNU General Public
// License along with Polypolish. If not, see <http://www.gnu.org/licenses/>.

use std::path::Path;
use std::path::PathBuf;
use std::fs::File;
use std::io;
use std::io::{prelude::*, BufReader};
use std::collections::HashSet;
use flate2::read::GzDecoder;


pub fn check_if_file_exists(filename: &PathBuf) {
    if !Path::new(filename).exists() {
        let error_message = format!("{:?} file does not exist", filename);
        quit_with_error(&error_message);
    }
}


pub fn quit_with_error(text: &str) {
    eprintln!();
    eprintln!("Error: {}", text);
    std::process::exit(1);
}

/// This function loads a FASTA file and runs a few checks on the result. If everything looks good,
/// it returns a vector of name+sequence tuples.
pub fn load_fasta(filename: &PathBuf) -> Vec<(String, String)> {
    let load_result = if is_file_gzipped(&filename) {
        load_fasta_gzipped(&filename)
    } else {
        load_fasta_not_gzipped(&filename)
    };
    match load_result {
        Ok(_) => ( ),
        Err(_) => quit_with_error(&format!("unable to load {:?}", filename)),
    }
    let fasta_seqs = load_result.unwrap();
    check_load_fasta(&fasta_seqs, &filename);
    fasta_seqs
}


/// This function looks at the result of the load_fasta function and does some checks to make sure
/// everything looks okay. If any problems are found, it will quit with an error message.
fn check_load_fasta(fasta_seqs: &Vec<(String, String)>, filename: &PathBuf) {
    if fasta_seqs.len() == 0 {
        quit_with_error(&format!("{:?} contains no sequences", filename));
    }
    for (name, sequence) in fasta_seqs {
        if name.len() == 0 {
            quit_with_error(&format!("{:?} has an unnamed sequence", filename));
        }
        if sequence.len() == 0 {
            quit_with_error(&format!("{:?} has an empty sequence", filename));
        }
    }
    let mut set = HashSet::new();
    for (name, _) in fasta_seqs {
        set.insert(name);
    }
    if set.len() < fasta_seqs.len() {
        quit_with_error(&format!("{:?} has a duplicated name", filename));
    }
}


/// This function returns true if the file appears to be gzipped (based on the first two bytes) and
/// false if not. If it can't open the file or read the first two bytes, it will quit with an error
/// message.
fn is_file_gzipped(filename: &PathBuf) -> bool {
    let open_result = File::open(&filename);
    match open_result {
        Ok(_) => ( ),
        Err(_) => quit_with_error(&format!("unable to open {:?}", filename)),
    }
    let file = open_result.unwrap();

    let mut reader = BufReader::new(file);
    let mut buf = vec![0u8; 2];

    let read_result = reader.read_exact(&mut buf);
    match read_result {
        Ok(_) => ( ),
        Err(_) => quit_with_error(&format!("{:?} is too small", filename)),
    }

    buf[0] == 31 && buf[1] == 139
}


fn load_fasta_not_gzipped(filename: &PathBuf) -> io::Result<Vec<(String, String)>> {
    let mut fasta_seqs = Vec::new();

    let file = File::open(&filename)?;
    let reader = BufReader::new(file);

    let mut name = String::new();
    let mut sequence = String::new();
    for line in reader.lines() {
        let text = line?;
        if text.len() == 0 {
            continue;
        }
        if text.starts_with('>') {
            if name.len() > 0 {
                fasta_seqs.push((name, sequence));
                sequence = String::new();
            }
            let first_piece = text[1..].split_whitespace().next();
            match first_piece {
                Some(_) => ( ),
                None => quit_with_error(&format!("{:?} is not correctly formatted", filename)),
            }
            name = first_piece.unwrap().to_string();
        } else {
            if name.len() == 0 {
                quit_with_error(&format!("{:?} is not correctly formatted", filename));
            }
            sequence.push_str(&text);
        }
    }
    if name.len() > 0 {
        fasta_seqs.push((name, sequence));
    }
    Ok(fasta_seqs)
}


fn load_fasta_gzipped(filename: &PathBuf) -> io::Result<Vec<(String, String)>> {
    let mut fasta_seqs = Vec::new();

    let file = File::open(&filename)?;
    let reader = BufReader::new(GzDecoder::new(file));

    let mut name = String::new();
    let mut sequence = String::new();
    for line in reader.lines() {
        let text = line?;
        if text.len() == 0 {
            continue;
        }
        if text.starts_with('>') {
            if name.len() > 0 {
                fasta_seqs.push((name, sequence));
                sequence = String::new();
            }
            let first_piece = text[1..].split_whitespace().next();
            match first_piece {
                Some(_) => ( ),
                None => quit_with_error(&format!("{:?} is not correctly formatted", filename)),
            }
            name = first_piece.unwrap().to_string();
        } else {
            if name.len() == 0 {
                quit_with_error(&format!("{:?} is not correctly formatted", filename));
            }
            sequence.push_str(&text);
        }
    }
    if name.len() > 0 {
        fasta_seqs.push((name, sequence));
    }
    Ok(fasta_seqs)
}