/**
 * CSS classes for /login /register /reset forms
 */
export function form_styles(): string {
  return `
    grid grid-cols-6 grid-rows-6 row-start-2 col-span-full row-span-full place-self-center w-full h-full rounded-b-3xl
    md:col-start-2 md:col-span-4
    lg:col-start-3 lg:col-span-2
    bg-secondary
  `
}
