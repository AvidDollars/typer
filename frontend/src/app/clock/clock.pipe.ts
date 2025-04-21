import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'clock'
})
export class ClockPipe implements PipeTransform {

  /**
   * Transforms elapsed time in seconds to a clock format.
   * E.g.: 15s -> 00:15; 666s -> 11:06.
   */
  transform(value: number | null): string { // TODO: "format" as the 2nd parameter?
    if (value == null) return "";

    const hrs = Math.floor(value / 3600);
    const hours = (hrs === 0) ? "" : `${hrs.toString().padStart(2, "0")}:`;

    // mm:ss
    const mins_secs = [Math.floor(value / 60), value % 60].map(String).map(value => value.padStart(2, "0"));

    // if at least 1 hour elapsed: "hh:mm:ss", "mm:ss" otherwise
    return `${hours}${mins_secs.join(":")}`;
  }
}
