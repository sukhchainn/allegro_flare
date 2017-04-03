#ifndef __PICKING_BUFFER_HEADER
#define __PICKING_BUFFER_HEADER




#include <allegro5/bitmap.h>




class PickingBuffer
{
private:
   ALLEGRO_BITMAP *surface_render;
   int w, h;

public:
   static const int ID_MAX = 16777216;

   PickingBuffer(int w, int h, int depth);
   ~PickingBuffer();

   void create_new_surface(int w, int h, int depth);
   void clear_surface();

   static ALLEGRO_COLOR encode_id(int id);
   static int decode_id(ALLEGRO_COLOR color);
   ALLEGRO_BITMAP *get_surface_render();
};




#endif
