#ifndef __AF_ELEMENT_ID_HEADER
#define __AF_ELEMENT_ID_HEADER



#include <vector>
#include <allegro_flare/attributes.h>

class ElementID : public Attributes
{
private:
   static int next_unique_id;
   int id;
   ElementID *parent;
   std::vector<ElementID *> children;

public:
   ElementID(ElementID *parent);
   ~ElementID();

   int get_id();
   int num_children();
   int num_descendants();

   ElementID *find_first(std::string attribute);
   ElementID *find_first(std::string attribute, std::string value);
   std::vector<ElementID *> find_all(std::string attribute);
   std::vector<ElementID *> find_all(std::string attribute, std::string value);
};




#endif
