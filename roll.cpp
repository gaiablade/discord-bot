#include <iostream>
#include <chrono>
#include <random>

extern "C" {
    uint64_t roll(uint64_t n) {
        std::mt19937 rng = std::mt19937(std::chrono::system_clock::now().time_since_epoch().count());

        return rng() % n + 1;
    }
}