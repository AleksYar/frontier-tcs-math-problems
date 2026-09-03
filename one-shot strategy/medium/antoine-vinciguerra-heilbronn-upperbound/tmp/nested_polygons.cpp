#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

struct Point { double x, y; };

static double area2(const Point& a, const Point& b, const Point& c) {
    return std::abs((b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x));
}

int main() {
    const double pi = std::acos(-1.0);
    const double frac = (std::sqrt(5.0)-1.0)/2.0;
    for (int m : {4,5,6,7,8,9,10,11,12}) {
        int layers = m*m;
        double period = 2*pi/m;
        double phi = frac*period;
        double reduced = std::min(phi, period-phi);
        double rho_tangent = std::cos(pi/m)/std::cos(pi/m-reduced);
        double rho = rho_tangent*(1.0-0.2/(m*m));
        std::vector<Point> p;
        for (int j=0; j<layers; ++j) {
            double r = 0.48*std::pow(rho,j);
            for (int k=0; k<m; ++k) {
                double th = j*phi + k*period;
                p.push_back({0.5+r*std::cos(th),0.5+r*std::sin(th)});
            }
        }
        double best = 1e100;
        int ai=0,bi=0,ci=0;
        for (int i=0; i<(int)p.size(); ++i)
            for (int j=i+1; j<(int)p.size(); ++j)
                for (int k=j+1; k<(int)p.size(); ++k) {
                    double a=0.5*area2(p[i],p[j],p[k]);
                    if (a<best) { best=a; ai=i; bi=j; ci=k; }
                }
        std::cout << m << " " << layers << " " << p.size() << " "
                  << std::setprecision(12) << rho << " " << best << " "
                  << best*layers*layers << " " << best*m*m*m << " "
                  << ai << "," << bi << "," << ci << "\n";
    }
}
