#include "Refract_Sph.h"

Refract_Sph::Refract_Sph(arr centre, double R, double start, double end, double n1, double n2)
	:	Spherical(centre, R, start, end), n1(n1), n2(n2)
{
}

void Refract_Sph::hit(Ray* ry, int n) const
{
	arr &r{ ry->pos.back() };
	arr &v{ ry->v };

	double t, tp;

	std::tie(t, tp) = solve(r, v);

	arr newPos;
	arr newV;

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	double angle{ tp - M_PI_2 };

	newV = rotate(v, angle);

	// angle of incidence
	double thetaI{ M_PI_2 - atan2(newV[1], newV[0]) };

	// Now we need to work out the initial and final refractive indices
	arr startRot{ rotate(newPos, angle) };
	arr rRot{ rotate(r, angle) };
	bool above{ false };
	double ni, nf;  // initial and final refractive indices

	if (rRot[1] >= startRot[1])
		above = true;

	if (above)
	{
		ni = n1;
		nf = n2;
	}
	else
	{
		ni = n2;
		nf = n1;
	}

	// Value of sin(thetaF) from Snell's law
	double s_thetaF{ ni*sin(thetaI) / nf };

	if (abs(s_thetaF) > 1)  // Check for total internal reflection
	{
		newV[1] = -newV[1];
	}
	else
	{
		double thetaF{ asin(s_thetaF) };

		newV[0] = sin(thetaF);

		if (above)
			newV[1] = -cos(thetaF);
		else
			newV[1] = cos(thetaF);
	}

	ry->pos.push_back(newPos);
	ry->v = rotate(newV, -angle);
}
