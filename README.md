# 2020 SKKU Graduation Project

## Member

- Junhyun Kim [@junbread](https://github.com/junbread)
- Hosung Ryu [@chrominium97](https://github.com/chrominium97)

## Topic

- Detect human sleeping habits using WiFi signals

## Tags

- none: 사람 없음
- still: 정자세로 가만히 누워 있음
- crouch: 새우잠
- flipped: 엎드려 잠
- rolling: 뒤척임

## Data Processing Pipeline

```txt
                <collector>

                     +
                     | Emits
                     v

          +----------------------+
          |Binary CSI data (.dat)|
          +----------------------+

                     +
                     |        For each tag,

              <preprocessor>  1) Merge .dat with same tag
                              2) Export them into single .npy
                     |
                     v

     +---------------------------------+
     |NumPy arrays (.npy)              |
     |                                 |
     |Amplitude and optional phase data|
     |                                 |
     |Shape: (pkts x 30) without phase |
     |       (pkts x 60) with    phase |
     +---------------------------------+

+--------------------+
|                    v
|                                Merge .npy files with same prefix
|             <classifier/data>  and split them into training and testing dataset (.pkl)
|
|                    |
|                    v
|
|   +-----------------------------------+
|   |Pickle exports (.pkl)              |
|   |                                   |
|   |Test and training dataset          |
|   |                                   |
|   |Test dataset:     dataset.test.pkl |
|   |Training dataset: dataset.train.pkl|
|   +-----------------------------------+
|
|                    +
|                    |
|                                 Train network from given dataset
|            <classifier/train>   and save model
|
|                    |
|                    v
|
|           +-----------------+
|           |Keras model (.h5)|
|           +-----------------+
|
|                    +
|                    |
|
+------->  <classifier/predict>

                     |
                     v

    +-----------------------------------+
    |List of predictions for each packet|
    +-----------------------------------+
```

```txt
still   4h  0400    4 * 3600 * 500  7200000
crouch  2h  0600    2 * 3600 * 500  3600000
rolling 2m  0602    2 * 60 * 500    60000
flip    30m 0632    30 * 60 * 500   900000
rolling 1m  0633    1 * 60 * 500    30000
still   1h  0733    1 * 3600 * 500  1800000
rolling 2m  0735    2 * 60 * 500    60000
still   25m 0800    25 * 60 * 500   750000
```
