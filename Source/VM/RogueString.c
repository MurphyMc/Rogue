//=============================================================================
//  RogueString.c
//
//  2015.08.30 by Abe Pralle
//=============================================================================
#include "Rogue.h"
#include <string.h>

RogueString* RogueString_create( RogueVM* vm, int count )
{
  int size = sizeof(RogueString) + count * sizeof(RogueCharacter);
  RogueString* THIS = (RogueString*) RogueObject_create( vm->type_String, size );
  THIS->count = size;
  return THIS;
}

RogueString* RogueString_from_utf8( RogueVM* vm, const char* utf8, int utf8_count )
{
  int decoded_count;
  RogueString* THIS;

  if (utf8_count == -1) utf8_count = strlen( utf8 );
  decoded_count = RogueUTF8_decoded_count( utf8, utf8_count );
  THIS = RogueString_create( vm, decoded_count );
  RogueUTF8_decode( utf8, utf8_count, THIS->characters, decoded_count );
  return RogueString_update_hash_code( THIS );
}

RogueString* RogueString_update_hash_code( RogueString* THIS )
{
  RogueCharacter* src = THIS->characters - 1;
  int hash_code = 0;
  int count = THIS->count;
  while (--count >= 0)
  {
    hash_code = ((hash_code << 3) - hash_code) + *(++src);
  }
  THIS->hash_code = hash_code;
  return THIS;
}

