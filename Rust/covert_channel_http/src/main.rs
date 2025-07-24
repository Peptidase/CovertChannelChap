use reqwest::Client;





fn main() {



    let heartbeat = "hello";
    let search_url = format!("http://www.google.com/search?q={}", heartbeat);


    let client = reqwest::Client::new();
    let res = client.post(search_url)
    .body("the exact body that is sent")
    .send();

}

