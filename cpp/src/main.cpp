#include <iostream>
#include <vector>
#include <fftw3.h> // This is the test. If CMake fails, this line errors.

int main() {
    std::cout << "--------------------------------" << std::endl;
    std::cout << "   Iron Age Engine: Online      " << std::endl;
    std::cout << "--------------------------------" << std::endl;

    // Sanity Check: Allocate FFTW complex array
    // This proves the linker found the library file (.so)
    fftw_complex* in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * 1024);
    
    if (in) {
        std::cout << "[PASS] FFTW3 Memory Allocation" << std::endl;
        
        // Always free manual memory!
        fftw_free(in); 
        std::cout << "[PASS] FFTW3 Memory Free" << std::endl;
    } else {
        std::cerr << "[FAIL] Critical Memory Error" << std::endl;
        return 1;
    }

    return 0;
}