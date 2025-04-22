/**
 * Service for fetching text from the backend
 */

import { HttpErrorResponse, httpResource } from '@angular/common/http';
import { computed, Injectable, signal } from '@angular/core';
import { environment } from '../../environment/environment';
import { Text } from './models';
import { retrieveErrorMessage } from '../user/shared';
import { toObservable } from '@angular/core/rxjs-interop';

@Injectable({
  providedIn: 'root'
})
export class TextLoaderService {

  textId = signal(environment.defaultTextId);
  private url = computed(() => environment.text(this.textId()));
  private textResource = httpResource<Text>(() => this.url()); // TODO: maybe use rxResource instead?

  text = computed(() => this.textResource.value()?.content);
  isLoading$ = toObservable(this.textResource.isLoading);

  error = computed(() => this.textResource.error() as HttpErrorResponse);
  errorMessage = computed<string | null>(() => {
    const error = this.error();
    return (error) ? retrieveErrorMessage(error) : null;
  });

  loadText(id: string) {
    this.textId.set(id);
  };
}
