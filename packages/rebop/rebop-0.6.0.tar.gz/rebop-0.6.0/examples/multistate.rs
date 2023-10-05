#![allow(non_snake_case)]
use rebop::define_system;

define_system! {
    kon koff kAon kAoff kAp kAdp;
    MultiState { R, L, RL, Au, AuR, AuRL, Ap, ApR, ApRL }
    r01 : R + L     => RL       @ kon
    r02 : RL        => R + L    @ koff
    r03 : R + Au    => AuR      @ kAon
    r04 : AuR       => R + Au   @ kAoff
    r05 : L + AuR   => AuRL     @ kon
    r06 : AuRL      => L + AuR  @ koff
    r07 : Au + RL   => AuRL     @ kAon
    r08 : AuRL      => Au + RL  @ kAoff
    r09 : AuRL      => ApRL     @ kAp
    r10 : ApRL      => AuRL     @ kAdp
    r11 : ApRL      => L + ApR  @ koff
    r12 : L + ApR   => ApRL     @ kon
    r13 : ApRL      => RL + Ap  @ koff
    r14 : RL + Ap   => ApRL     @ kon
    r15 : R + Ap    => ApR      @ kAon
    r16 : ApR       => R + Ap   @ kAoff
    r17 : ApR       => AuR      @ kAdp
    r18 : Ap        => Au       @ kAdp
}

fn main() {
    let mut num = Vec::new();
    for _ in 0..10000 {
        let mut problem = MultiState::new();
        problem.R = 5360;
        problem.L = 1160;
        problem.Au = 5360;
        problem.kon = 0.01;
        problem.koff = 0.1;
        problem.kAon = 0.01;
        problem.kAoff = 0.1;
        problem.kAp = 0.01;
        problem.kAdp = 0.1;
        problem.advance_until(10.);
        num.push(problem.Au);
    }
    println!("{}", num.iter().sum::<isize>() as f64 / num.len() as f64);
}
