const neo4j = require('neo4j-driver')

const boltURL = 'bolt://18.206.127.86:7687'
const username = 'neo4j'
const password = 'crack-buy-intensities'

async function queryPerson(personName) {
  const driver = neo4j.driver(
    boltURL,
    neo4j.auth.basic(username, password))
  
  const session1 = driver.session({
    database: 'neo4j',
  })
  
  const res = await session1.readTransaction( tx => {
    return tx.run(
      `MATCH (p:Person)
      WHERE p.name Contains $name
      RETURN p
      LIMIT 4`,
      { name: personName }
    )
  })

  const names = res.records.map( row => {
    return [row.get('p')['properties']['name'], row.get('p')['properties']['born']]
  })
  
  await session1.close()
  
  await driver.close()

  return names
}

async function queryMovie(movieName) {
  const driver = neo4j.driver(
    boltURL,
    neo4j.auth.basic(username, password))
  
  const session1 = driver.session({
    database: 'neo4j',
  })
  
  const res = await session1.readTransaction( tx => {
    return tx.run(
      `MATCH (m:Movie)
      WHERE m.title Contains $title
      RETURN m
      LIMIT 4`,
      { title: movieName }
    )
  })
  
  const names = res.records.map( row => {
    return [row.get('m')['properties']['title'], row.get('m')['properties']['tagline']]
  })
  
  await session1.close()
  
  await driver.close()
  
  return names
}

async function queryMovieDetail(movieName) {
  const driver = neo4j.driver(
    boltURL,
    neo4j.auth.basic(username, password))
  
  const session1 = driver.session({
    database: 'neo4j',
  })
  
  const res = await session1.readTransaction( tx => {
    return tx.run(
      `MATCH (m:Movie)
      WHERE m.title Contains $title
      RETURN m
      LIMIT 1`,
      { title: movieName }
    )
  })

  const names = res.records.map( row => {
    return [row.get('m')['properties']['title'], row.get('m')['properties']['tagline'], String(row.get('m')['properties']['released'])]
  })
  
  await session1.close()
  
  await driver.close()
  
  return names
}

module.exports = {
  queryPerson,
  queryMovie,
  queryMovieDetail
}