#include "Complex_Component.h"

double Complex_Component::test_hit(Ray* ry) const
{
	std::vector<double> t;  // Vector to store hitting times

	for (auto &c : comps)
		t.push_back(c->test_hit(ry));

	size_t ind{ next_component(t) };  // Returns index of next component, -1 if none

	if (ind == -1)
		return -1.0;
	else
		return t[ind];
}

void Complex_Component::hit(Ray* ry, int n) const
{
	trace_ray(comps, ry, n);
}
