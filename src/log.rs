// Copyright 2021 Ryan Wick (rrwick@gmail.com)
// https://github.com/rrwick/Polypolish

//This file is part of Polypolish. Polypolish is free software: you can redistribute it and/or
// modify it under the terms of the GNU General Public License as published by the Free Software
// Foundation, either version 3 of the License, or (at your option) any later version. Polypolish
// is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
// implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
// Public License for more details. You should have received a copy of the GNU General Public
// License along with Polypolish. If not, see <http://www.gnu.org/licenses/>.

use chrono::prelude::*;
use colored::Colorize;


pub fn section_header(text: &str) {
    colored::control::set_override(true);
    let now = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
    let date = format!("({})", now);
    eprintln!();
    eprintln!("{} {}", text.bold().bright_yellow().underline(), date.dimmed());
    colored::control::unset_override();
}


pub fn explanation(text: &str) {
    colored::control::set_override(true);
    let mut term_width = 80;
    if let Some((w, _)) = term_size::dimensions_stderr() {
        term_width = w;
    }
    let indented_text = format!("    {}", text);
    eprintln!("{}", textwrap::fill(&indented_text, term_width).dimmed());
    eprintln!();
    colored::control::unset_override();
}
