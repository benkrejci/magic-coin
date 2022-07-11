const _ = require('lodash')

const vals = (a) => a.map((bit, i) => (bit ? i : 0))
const calc = (a) => vals(a).reduce((prev, curr) => prev ^ curr)
const gen = (n) => _.range(0, n).map(() => (Math.random() > 0.5 ? 1 : 0))
const flip = (a, flipIndex) =>
  a.map((v, i) => (i === flipIndex ? Number(!v) : v))
const toBinary = (v, maxV) =>
  `${_.repeat(
    '0',
    Math.ceil(Math.log2(maxV + 1)) - (v === 0 ? 1 : Math.ceil(Math.log2(v + 1)))
  )}${Number(v).toString(2)}`
const printGrid = (a, magicIndex) => {
  const root = Math.sqrt(a.length)
  const maxLength = a.reduce((p, c) => Math.max(p, String(c).length), 0)
  console.log(
    a
      .map((v, i) => {
        const currIsMagic = i === magicIndex
        const prevIsMagic = i - 1 === magicIndex
        const isNewLine = !(i % root)
        return `${isNewLine && i ? '\n' : ''}${
          currIsMagic ? '(' : prevIsMagic && !isNewLine ? '' : ' '
        }${v}${currIsMagic ? ')' : ''}${_.repeat(
          ' ',
          maxLength - String(v).length
        )}`
      })
      .join('') + '\n'
  )
}

const tryEach = (a) =>
  _.range(0, a.length).map((flipIndex) => calc(flip(a, flipIndex)))

const tryRandomGrid = (gridSize, verbose = true) => {
  const allHeads = _.range(0, gridSize).map((i) => i)
  if (verbose) {
    console.log(`All heads grid:`)
    printGrid(allHeads)
    console.log(`All heads binary grid:`)
    printGrid(allHeads.map((v) => toBinary(v, gridSize - 1)))
  }

  const a = gen(gridSize)
  const magicIndex = Math.round(Math.random() * (gridSize - 1))

  if (verbose) {
    console.log(
      `Magic index: ${magicIndex} [${toBinary(magicIndex, gridSize - 1)}]`
    )
    console.log(`Initial coins state:`)
    printGrid(a, magicIndex)
    console.log(`Coin values:`)
    printGrid(vals(a), magicIndex)
    console.log(`Coin values in binary:`)
    printGrid(
      vals(a).map((v) => toBinary(v, gridSize - 1)),
      magicIndex
    )
  }

  const result = calc(a)

  verbose &&
    console.log(`Initial result: ${result} [${toBinary(result, gridSize - 1)}]`)

  const toFlip = result ^ magicIndex

  verbose &&
    console.log(
      `To implicate magic coin, flip index: ${toFlip} [${toBinary(
        toFlip,
        gridSize - 1
      )}]`
    )

  const flipped = flip(a, toFlip)
  const flippedResult = calc(flipped)

  if (verbose) {
    console.log(
      `Result after flip: ${flippedResult} [${toBinary(
        flippedResult,
        gridSize - 1
      )}]`
    )
    console.log(
      `Result after flip matches magic index: ${flippedResult === magicIndex}`
    )
  }

  return flippedResult === magicIndex
}

const tryRandomGrids = (numGrids, gridSize) => {
  console.log(`Trying grids...`)

  let matches = 0
  _.times(numGrids, () => {
    const match = tryRandomGrid(gridSize, false)
    if (match) matches++
  })

  console.log(
    `Valid solution found ${
      (matches / numGrids) * 100
    }% of ${numGrids.toLocaleString()} ${gridSize}x${gridSize} grids`
  )
}

module.exports = {
  tryEach,
  tryRandomGrid,
  tryRandomGrids,
}
