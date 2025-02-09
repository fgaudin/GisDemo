import type ISpecies from "./Species"

export default interface IObservation {
  id: number
  date: string
  lattitude: string
  longitude: string
  species: ISpecies
}