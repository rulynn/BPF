## README

#### FILE

```
criticality_stacks: Implemented critical stacks
    - dataprocess.py: Process the acquired data and draw a critical stack diagram
    - dataprocess_old.py: old version
    - locktime.c: eBPF
    - locktime.py: eBPF
    - run.sh: Run command for Critical Stacks
    - run_profile.sh: Run command for stack trace
    - run_stat.sh: Run command for Flamegraph
java: simple java program
learn: resources
```

#### RUN

```bash
# download the code
git clone https://github.com/rulynn/Master-Project.git
git checkout feature

cd criticality_stacks/
# sh run.sh $time (time means duration of program sampling)
sh run.sh 5
```

#### Result

Result shows in `out.log` and `out/`

```
out.log: log
out/
	- critical.png: critical stacks
	- threads.png: Wait time and hold time of each thread
```

###### Example

`out.log`

```
--- pid 336 ---
	 mtx 139827425887528 ::: start time 0.00us ::: wait time 87.71us ::: hold time 91.73us
	 mtx 139827425362984 ::: start time 64.83us ::: wait time 41.56us ::: hold time 6851.74us
--- pid 344 ---
	 mtx 139827426190888 ::: start time 1791091.70us ::: wait time 9.09us ::: hold time 0.00us
--- pid 346 ---
	 mtx 139827425887528 ::: start time 699109.60us ::: wait time 12.12us ::: hold time 11.41us
	 mtx 139827539771264 ::: start time 1711093.63us ::: wait time 33.20us ::: hold time 15.02us
	 mtx 139827426213160 ::: start time 3637.62us ::: wait time 1401.11us ::: hold time 4968992.26us
--- pid 339 ---
	 mtx 139827425362984 ::: start time 3563.82us ::: wait time 69.19us ::: hold time 59.86us
	 mtx 139827425887528 ::: start time 3602.45us ::: wait time 70.17us ::: hold time 4813210.79us
--- pid 343 ---
	 mtx 139827426182696 ::: start time 1806091.03us ::: wait time 11.32us ::: hold time 0.00us
```

`out/critical.png`

<img src=https://linoy.oss-cn-beijing.aliyuncs.com/critical.png width=300px>

#### QUESTION

- How to deal with the situation where the hold time is very large, the criticality of the thread accounts for a large proportion, for example pid 346
- How to deal with a thread holding two locks at the same time, for example pid 339