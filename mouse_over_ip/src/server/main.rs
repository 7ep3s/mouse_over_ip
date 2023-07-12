use std::net::{UdpSocket};
use std::string::String;

use evdev::*;

use serde::{Serialize,Deserialize};
use serde_json::Result;
use serde_json::json;
//use serde_json::Value::String;

mod _pick_device;

//made this so it's easy to serialize and deserialize input_events because that is not implemented in evdev on the top level...
#[derive(Serialize,Deserialize,Debug)]
struct moip_event {
    type_: u16,
    code: u16,
    value: i32,
}

fn main() {
    let socket = UdpSocket::bind("0.0.0.0:50000").expect("coulnd't bind to address");
    println!("socket bound");


    let mut counter = 0u32;

    let mut d = _pick_device::pick_device();

    loop {
            for ev in d.fetch_events().unwrap() {
                let ref_ = ev.as_ref();
                let asd = moip_event{
                    type_ : ref_.type_,
                    code  : ref_.code,
                    value : ref_.value,
                };
                //testing serializing and deserializing input events. timestamp is omitted for now becase cba lol
                let bytes = bincode::serialize(&asd).unwrap();
                //print debug of evdev inputevent
                println!("{:?}", ev);
                //serialized bytestream
                println!("{:?}", bytes);
                //kutya means dog, we sometimes call things kutya when angry
                let kutya: moip_event = bincode::deserialize(&bytes).unwrap();
                //raw moip_event struct
                println!("{:?}", asd);
                //deserialized moip_event struct, should be the same if the raw one...
                println!("{:?}", kutya);
                


                //let _ = socket.send_to(&bytes,"192.168.1.162:50000");
                //println!("{:?}",asd);
            }
        }
        //println!("{}",message);
        //let _ = socket.send_to(&message_u,"192.168.1.162:50000");
        //if counter >= 10 {break;}
    //socket.send_to(&message_u,"192.168.1.162:50000");
}