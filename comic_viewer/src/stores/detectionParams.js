import { reactive } from "vue";

export const detectionParams = reactive({
  blur: 5,
  threshold: 100,
  morph: 5,
  minSize: 10,
  bubbleThreshold: 150,
  bubbleMin: 0.0001,
  bubbleMax: 0.1,
  minCircularity: 0.4
});
