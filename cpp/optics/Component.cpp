#include "Component.h"

arr Component::rotate(const arr &r, const double theta) const
{
	double top{ cos(theta)*r[0] + sin(theta)*r[1] };
	double bottom{ -sin(theta)*r[0] + cos(theta)*r[1] };

	return { top, bottom };
}

double Component::compute_t(const arr & r, const arr & v, const arr & pos) const
{
	int ind{ 0 };

	if (abs(v[1]) > 0.5)
		ind = 1;

	return (pos[ind] - r[ind]) / v[ind];
}

std::ostream & operator<<(std::ostream & os, const Component & b)
{
	b.print(os);
	return os;
}
