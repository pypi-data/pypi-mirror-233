#include <pyopencl-complex.h>
typedef cfloat_t complex;


/* 
  In-place one-dimensional fftshift, along fast (horizontal) dimension.
  The array can be 1D or 2D.
*/
__kernel void fftshift1(
    __global DTYPE* array,
    int Nx,
    int Ny
) {
    int x = get_global_id(0), y = get_global_id(1);
    int N2 = Nx >> 1;
    int N2b = Nx - N2;
    if (x >= N2b || y >= Ny) return;
    DTYPE tmp = array[y*Nx + x];
    if (x < N2) array[y*Nx + x] = array[y*Nx + N2b + x]
    array[y*Nx + N2 + x] = tmp
}



