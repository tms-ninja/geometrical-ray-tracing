#include "Complex_Component.h"

double Complex_Component::test_hit(Ray* ry) const
{
	std::vector<double> t;  // Vector to store hitting times

	for (auto &c : comps)
		t.push_back(c->test_hit(ry));

	size_t ind;
	bool found;

	std::tie(ind, found) = next_component(t);

	return found ? t[ind] : -1.0;
}

void Complex_Component::hit(Ray* ry, int n) const
{
	trace_ray(comps, ry, n);
}
