#include<complex>
#include<iostream>
using namespace std;
typedef complex<double> cpx;
#define N 8
#define PI 3.1415926

cpx omega [N], omegaInverse [N] ;

void init ( const int& n )  {
    for ( int i = 0 ; i < n ; ++ i )  {
        omega [i] = cpx ( cos ( 2 * PI / n * i), sin ( 2 * PI / n * i ) ) ;
        omegaInverse [i] = omega [i] ;
        cout<<omega[i]<<endl;
    }
}

void transform ( cpx *a, const int& n, const cpx* omega ) {
    for ( int i = 0, j = 0 ; i < n ; ++ i )  {
        if ( i > j )  std :: swap ( a [i], a [j] ) ;
        for( int l = n >> 1 ; ( j ^= l ) < l ; l >>= 1 ) ;
    }

    for ( int l = 2 ; l <= n ; l <<= 1 )  {
        int m = l / 2;
        for ( cpx *p = a ; p != a + n ; p += l )  {
            for ( int i = 0 ; i < m ; ++ i )  {
                cpx t = omega [n / l * i] * p [m + i] ;
                p [m + i] = p [i] - t ;
                p [i] += t ;
            }
        }
    }
}

void dft ( cpx *a, const int& n )  {
    transform ( a, n, omega ) ;
}

void idft ( cpx *a, const int& n )  {
    transform ( a, n, omegaInverse ) ;
    for ( int i = 0 ; i < n ; ++ i ) a [i] /= n ;
}

int main () {
    double beg=omp_get_wtime();
    init(N);
    dft(omegaInverse, N);
    for ( int i = 0 ; i < N ; ++ i )  {
        cout<<omega[i]<<omegaInverse[i]<<endl;
    }
}