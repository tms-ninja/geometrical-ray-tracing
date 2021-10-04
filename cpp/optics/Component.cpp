#include "Component.h"

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
