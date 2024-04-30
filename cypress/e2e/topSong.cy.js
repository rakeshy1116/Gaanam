describe('cypress tests', () => {
  it('renders home page', () => {
    cy.visit('http://localhost:3000')
    cy.get('[data-testid="cypress-test-button"]').should('exist')
    .should('have.text', 'Login with Spotify')
  })

  // it('login button works', () => {
  //   cy.visit('http://localhost:3000')
  //   cy.get('[data-testid="cypress-test-button"]').click()
  //   cy.url().should('include', 'https://accounts.spotify.com/authorize')
  // })

  it('get top song button works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopSong"]').should('exist')
    .should('have.text', 'Show Top Songs')
  
  })

  it('click top song button 4 weeks works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopSong"]').click()
    cy.get('[data-testid="cypress-gettopSong4weeks"]').should('exist')
    cy.get('[data-testid="cypress-gettopSong4weeks"]').click()
    cy.wait(1000)
    cy.get('[data-testId="cypress-topSong-Image"]').should('exist')
    .should('have.text', 'Image')
    cy.get('[data-testId="cypress-topSong-SongName"]').should('exist')
    .should('have.text', 'Song Name')
    cy.get('[data-testId="cypress-topSong-Artist"]').should('exist')
    .should('have.text', 'Artist')
    cy.get('[data-testId="cypress-topSong-Preview"]').should('exist')
    .should('have.text', 'Preview')
    cy.get('[data-testId="cypress-topSong-Play"]').should('exist')
    .should('have.text', 'Play')
    cy.get('[data-testId="cypress-topSong-AddButton"]').should('exist')
    cy.get('[data-testId="cypress-topSong-Table"]').should('exist')
    
  })

  it('click top song button 6 months works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopSong"]').click()
    cy.get('[data-testid="cypress-gettopSong6months"]').should('exist')
    cy.get('[data-testid="cypress-gettopSong6months"]').click()
    cy.wait(1000)
    cy.get('[data-testId="cypress-topSong-Image"]').should('exist')
    .should('have.text', 'Image')
    cy.get('[data-testId="cypress-topSong-SongName"]').should('exist')
    .should('have.text', 'Song Name')
    cy.get('[data-testId="cypress-topSong-Artist"]').should('exist')
    .should('have.text', 'Artist')
    cy.get('[data-testId="cypress-topSong-Preview"]').should('exist')
    .should('have.text', 'Preview')
    cy.get('[data-testId="cypress-topSong-Play"]').should('exist')
    .should('have.text', 'Play')
    cy.get('[data-testId="cypress-topSong-AddButton"]').should('exist')
    cy.get('[data-testId="cypress-topSong-Table"]').should('exist')
    
  })

  it('add playlist button works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopSong"]').click()
    cy.get('[data-testid="cypress-gettopSong12months"]').should('exist')
    cy.get('[data-testid="cypress-gettopSong12months"]').click()
    cy.wait(2000)
    cy.get('[data-testid="cypress-addplaylist-button"]').should('exist')
    .should('have.text', 'Add Selected Songs')
  })

  it('click top song button 12 months works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopSong"]').click()
    cy.get('[data-testid="cypress-gettopSong12months"]').should('exist')
    cy.get('[data-testid="cypress-gettopSong12months"]').click()
    cy.wait(1000)
    cy.get('[data-testId="cypress-topSong-Image"]').should('exist')
    .should('have.text', 'Image')
    cy.get('[data-testId="cypress-topSong-SongName"]').should('exist')
    .should('have.text', 'Song Name')
    cy.get('[data-testId="cypress-topSong-Artist"]').should('exist')
    .should('have.text', 'Artist')
    cy.get('[data-testId="cypress-topSong-Preview"]').should('exist')
    .should('have.text', 'Preview')
    cy.get('[data-testId="cypress-topSong-Play"]').should('exist')
    .should('have.text', 'Play')
    cy.get('[data-testId="cypress-topSong-AddButton"]').should('exist')
    cy.get('[data-testId="cypress-topSong-Table"]').should('exist')
  })
  
})