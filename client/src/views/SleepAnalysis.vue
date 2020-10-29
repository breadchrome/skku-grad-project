<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>수면 분석</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">수면 분석</ion-title>
        </ion-toolbar>
        <ion-toolbar>
          <ion-searchbar placeholder="검색할 날짜를 입력하세요."></ion-searchbar>
        </ion-toolbar>
      </ion-header>

      <ion-card v-if="loaded">
        <ion-card-header>
          <ion-card-subtitle>수면 패턴</ion-card-subtitle>
          <ion-card-title>오늘</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <p>{{ sleepStartHour }}에 수면을 시작했습니다.</p>
          <p>{{ sleepHours.toFixed(2) }} 시간동안 수면을 취했습니다.</p>
          <apex-charts
            width="100%"
            :options="options"
            :series="series"
          ></apex-charts>
          <p>
            안정된 수면을 기록했습니다. 새우잠은 척추 건강에 좋지 않을 수
            있습니다.
          </p>
        </ion-card-content>
      </ion-card>
    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonSearchbar
} from '@ionic/vue';
import ApexCharts from '../components/ApexCharts';
import dayjs from 'dayjs';
import _ from 'lodash';

export default {
  name: 'SleepAnalysis',
  components: {
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonPage,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonSearchbar,
    ApexCharts,
  },
  data() {
    return {
      loaded: false,
      options: {
        chart: {
          height: 200,
          type: 'rangeBar',
          toolbar: {
            show: false,
          },
        },
        xaxis: {
          show: false,
          type: 'datetime',
          labels: {
            show: false,
          },
          axisBorder: {
            show: false,
          },
        },
        yaxis: {
          show: false,
          labels: {
            show: false,
          },
          axisBorder: {
            show: false,
          },
        },
        grid: {
          show: false,
        },
        fill: {
          type: 'solid',
        },
        tooltip: {
          enabled: false,
        },
        plotOptions: {
          bar: {
            horizontal: true,
            barHeight: '50%',
            rangeBarGroupRows: true,
          },
        },
      },
      series: [],
      sleepHours: null,
      sleepStartHour: null
    };
  },
  async created() {
    const { data } = await this.$http.get(
      'http://localhost:8088/sleeping-analysis',
      {
        params: {
          user: 'test',
          date: dayjs().format('YYYY-MM-DD'),
          max_timeline_len: 100,
        },
      }
    );

    const tick = data.tick;
    const tags = data.tags;

    let currentTime = dayjs(data.start);
    const timeline = _.groupBy(
      data.timeline.map((t) => {
        const tick_obj = {
          x: 'time',
          y: [currentTime.valueOf(), currentTime.add(tick, 'ms').valueOf()],
          name: tags[t],
        };
        currentTime = currentTime.add(tick, 'ms');

        return tick_obj;
      }),
      'name'
    );

    let series = [];
    for (const [name, data] of Object.entries(timeline)) {
      series.push({ name, data });
    }

    this.series = series;
    this.sleepHours = (tick * data.timeline.length / (3600 * 1000));
    this.sleepStartHour = dayjs(data.start).format('MM월 DD일 HH시 mm분');
    this.loaded = true;
  },
};
</script>
