import type ISpecies from "./Species"

export default interface IObservation {
  id: number
  date: string
  latitude: string
  longitude: string
  count: number
  species: ISpecies
}