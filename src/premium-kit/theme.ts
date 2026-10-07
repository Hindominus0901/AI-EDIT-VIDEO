import sets from './sets.json';
export type PremiumSet = keyof typeof sets;
export const premiumSets = sets;
export type PremiumTheme = typeof sets[PremiumSet];
