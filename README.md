# Hermes

**Hermes** is the Greek god of messengers, communication, commerce, and travel. Often depicted with winged sandals, he is known for his speed, wit, and ability to move freely between the realms of gods and mortals.  

### Build

Assemble toolchain first by  

```
sudo python3 Tools/toolchian.py
```

Build target for x86_64  
```
cmake --preset x86_64-release
ninja -C build/x86_64-release/ all
```

Build target for aarch64  
```
cmake --preset aarch64-release
ninja -C build/aarch64-release/ all
```