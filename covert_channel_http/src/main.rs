use reqwest::blocking::Client;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let client = Client::new();
    let resp = client
        .get("https://www.rust-lang.org")
        .send()?;

    println!("Status: {}", resp.status());
    let body = resp.text()?;
    println!("Body:\n{}", body);

    Ok(())
}