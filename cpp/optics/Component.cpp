#include "Component.h"

std::ostream & operator<<(std::ostream & os, const Component & b)
{
	b.print(os);
	return os;
}
