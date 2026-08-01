---
name: radare2
description: Use when analyzing binary files, reverse engineering, disassembling executables, debugging, patching binaries, CTF challenges, malware analysis, or inspecting ELF/PE/Mach-O file structure. Triggers: "analyze this binary", "reverse this", "disassemble", "what does this exe do", "CTF binary", "patch this file", "check for strings in binary", "find the password in this executable".
---

# radare2

Reverse engineering framework. Analyze, disassemble, debug, and patch binaries. Installed at `C:\Users\44527\radare2\radare2-6.1.8-w64\bin\`.

## Quick Reference

| Task | Command |
|------|---------|
| Open with auto-analysis | `r2 -A <file>` |
| Open write mode (patching) | `r2 -w <file>` |
| Open without analysis | `r2 <file>` |
| Run command and quit | `r2 -A -q -c "<cmd>" <file>` |

## Essential Interactive Commands

Once inside `[0x...]>` prompt:

### Analysis
| Command | Action |
|---------|--------|
| `aaa` | Full auto-analysis |
| `afl` | List all functions |
| `afl~keyword` | Filter functions by name |
| `afn new_name` | Rename current function |

### Navigation
| Command | Action |
|---------|--------|
| `s main` | Seek to main |
| `s sym.func_name` | Seek to named function |
| `s 0x401000` | Seek to address |
| `s` | Print current address |

### Disassembly
| Command | Action |
|---------|--------|
| `pdf` | Disassemble current function |
| `pdc` | Pseudo-C decompilation |
| `pd 20` | Disassemble 20 instructions |
| `VV` | Visual graph mode (Tab=switch, q=quit) |
| `VV @ sym.func` | Visual graph for specific function |

### Information Gathering
| Command | Action |
|---------|--------|
| `ii` | Import table (DLL functions used) |
| `iE` | Export table |
| `iz` | Strings in binary |
| `iz~keyword` | Search strings for keyword |
| `i~pic` | Security features (PIE/NX/RELRO/canary) |
| `iS` | Sections with permissions |
| `iH` | File header |
| `ie` | Entry point |

### Search
| Command | Action |
|---------|--------|
| `/ password` | Search string |
| `/x 9090` | Search hex bytes |
| `/c xor eax` | Search for instruction pattern |

### Cross-References
| Command | Action |
|---------|--------|
| `axt @ addr` | Who references this address |
| `axf @ addr` | What this address references |

### Data Viewing
| Command | Action |
|---------|--------|
| `px 64 @ addr` | Hex dump 64 bytes |
| `ps @ addr` | Print as string |
| `pd 10 @ addr` | Disassemble 10 at address |

### Patching (requires `-w` flag)
| Command | Action |
|---------|--------|
| `s addr` then `wx 90 90` | Write NOP bytes |
| `s addr` then `wa jmp 0x401200` | Write assembly |
| `s addr` then `w hello\0` | Write string |

### Annotations
| Command | Action |
|---------|--------|
| `CC comment text` | Add comment at cursor |
| `CCa comment text @ addr` | Add comment at address |

## One-Shot Commands (No Interactive Mode)

Best for Claude to run single queries:

```bash
# List all functions
r2 -A -q -c "afl" target.exe

# Search strings for keyword
r2 -A -q -c "iz~password" target.exe

# Get imports
r2 -A -q -c "ii" target.exe

# Security checks
r2 -A -q -c "i~pic" target.exe

# Disassemble a function
r2 -A -q -c "s sym.main; pdf" target.exe

# Entry point info
r2 -A -q -c "ie" target.exe

# File header & compiler info
r2 -A -q -c "iH" target.exe

# All sections
r2 -A -q -c "iS" target.exe

# Disassemble with pseudo-C
r2 -A -q -c "s sym.main; pdc" target.exe
```

Chain multiple queries with `;`:
```bash
r2 -A -q -c "ie; i~pic; ii; iz~key" target.exe
```

## CTF Workflow

```bash
# 1. Reconnaissance
r2 -A -q -c "iH; i~pic; ie; iS" ./chall

# 2. Find interesting strings
r2 -A -q -c "iz~correct; iz~flag; iz~password; iz~wrong" ./chall

# 3. Find functions referencing those strings
r2 -A -q -c "axt @@=`iz~flag[1]`" ./chall

# 4. Disassemble the validation function
r2 -A -q -c "s sym.check_flag; pdf" ./chall

# 5. Decompile to pseudo-C
r2 -A -q -c "s sym.check_flag; pdc" ./chall
```

## Common Mistakes

- **Forgetting `-A`**: Without `-A`, no auto-analysis — `afl` returns nothing, `pdf` on unknown function fails. Always run `aaa` or use `-A`.
- **Windows path backslashes**: Always use forward slashes or double-backslashes in r2.
- **Analyzing large binaries without limit**: `aaa` on >100MB binaries can hang. Use `aa` (basic) first.
- **Not checking security features first**: Always `i~pic` before diving into logic — tells you what mitigations are in play.
