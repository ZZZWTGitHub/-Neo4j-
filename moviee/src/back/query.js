const neo4j = require('neo4j-driver')

async function queryPerson(personName) {
  const driver = neo4j.driver(
    'bolt://54.227.217.146:7687',
    neo4j.auth.basic('neo4j', 'patrol-molecules-flush'))
  
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
    // console.log(row.get('p')['properties']['name'])
    // console.log('---------------')
    return [row.get('p')['properties']['name'], row.get('p')['properties']['bio']]
  })
  
  // console.log(res.records[0].get('tom'))
  // console.log(names)
  
  await session1.close()
  
  // console.log('end')
  
  await driver.close()
  
  // console.log('end 2')

  // console.log(names)
  return names
}

async function queryMovie(movieName) {
  const driver = neo4j.driver(
    'bolt://54.227.217.146:7687',
    neo4j.auth.basic('neo4j', 'patrol-molecules-flush'))
  
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
    // console.log(row.get('m'))
    // console.log('---------------')
    return [row.get('m')['properties']['title'], row.get('m')['properties']['plot']]
  })
  
  await session1.close()
  
  await driver.close()
  
  return names
}

module.exports = {
  queryPerson,
  queryMovie
}