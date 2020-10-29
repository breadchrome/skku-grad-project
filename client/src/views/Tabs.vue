<template>
  <ion-page>
    <ion-tabs>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="tab1" href="/sleep-analysis">
          <ion-icon :icon="bed" />
          <ion-label>수면 분석</ion-label>
        </ion-tab-button>
          
        <ion-tab-button tab="tab2" href="/settings">
          <ion-icon :icon="cog" />
          <ion-label>설정</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script>
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage } from '@ionic/vue';
import { cog, bed, settings } from 'ionicons/icons';

export default {
  name: 'Tabs',
  components: { IonLabel, IonTabs, IonTabBar, IonTabButton, IonIcon, IonPage },
  setup() {
    return {
      cog,
      bed,
      settings,
    }
  }
}
</script>