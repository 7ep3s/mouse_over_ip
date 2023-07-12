use std::net::{UdpSocket};
use std::string::String;

use serde::{Serialize,Deserialize};

//made this so it's easy to serialize and deserialize input_events because that is not implemented in evdev on the top level...
#[derive(Serialize,Deserialize,Debug)]
struct moip_event {
    type_: u16,
    code: u16,
    value: i32,
}

fn main {
    let socket = UdpSocket::bind("0.0.0.0:50000").expect("coulnd't bind to address");
    println!("socket bound");

    loop{
        let mut buf = [0; 100];
        let (amt, src) = socket.recv_from(&mut buf)?;
        let packet: moip_event = bincode::deserialize(&bytes).unwrap();
        println!("{:?}",packet);
    }

}