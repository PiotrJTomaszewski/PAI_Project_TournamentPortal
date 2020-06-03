class ParticipantSVG {
    constructor(centerPositionX, centerPositionY, userName, avatarAddress) {
      const boxWidth = 100;
      const boxHeight = 60;
      const positionX = centerPositionX - boxWidth/2;
      const positionY = centerPositionY - boxHeight/2;
      const avatarSize = 40;
      const padding = 10;
      const avatarPositionX = positionX + padding;
      const avatarPositionY = positionY + padding;
      const textPositionX = positionX + avatarSize + 2*padding;
      const textPositionY = positionY + boxHeight/2;
      this.html = `<rect x="${positionX}" y="${positionY}" width="${boxWidth}" height="${boxHeight}" style="fill:none;stroke:#000000"/><text x="${textPositionX}" y="${textPositionY}" fill="#000000">${userName}</text><image href="${avatarAddress}" height="${avatarSize}" width="${avatarSize}" x="${avatarPositionX}" y="${avatarPositionY}"/>`;
      this.attachNode = {
        left: {
          x: positionX,
          y: positionY + (boxHeight / 2)
        },
        right: {
          x: positionX + boxWidth,
          y: positionY + (boxHeight / 2)
        }
      }
    }
  }
  
  class BrokenLine {
    constructor(from, to) {
      const diffX = to.x - from.x;
      const diffY = to.y - from.y;
      const halfX = from.x + diffX/2;
      this.html = `<path fill="none" stroke="#000000" d="M${from.x} ${from.y} L${halfX} ${from.y} V${to.y} L${to.x} ${to.y}"/>`
    }
  }
  
  class TournamentBracket {
    directions = {left: 0, right: 1}
    constructor(participants, results, drawRegionSize) {
      this.entryWidth = 120;
      this.entryHeight = 100;
      const roundsNo = 4;
      const posX = drawRegionSize.width / 2;
      const posY = drawRegionSize.height / 2;
      var winner = new ParticipantSVG(posX, posY, 'user', 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?f=y');
      var finalist0posX = posX - this.entryWidth;
      var finalist1posX = posX + this.entryWidth;
      var finalist0 = new ParticipantSVG(finalist0posX, posY, 'user', 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?f=y');
      var finalist1 = new ParticipantSVG(finalist1posX, posY, 'user', 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?f=y');
  
      this.svgHtml = winner.html + finalist0.html + finalist1.html
        + new BrokenLine(finalist0.attachNode.right, winner.attachNode.left).html
        + new BrokenLine(winner.attachNode.right, finalist1.attachNode.left).html
        + this.generateBracketLevel(roundsNo-1, finalist0posX-this.entryWidth, 0, posY, finalist0.attachNode.left, this.directions.left)
        + this.generateBracketLevel(roundsNo-1, finalist0posX-this.entryWidth, posY, drawRegionSize.height, finalist0.attachNode.left, this.directions.left)
        + this.generateBracketLevel(roundsNo-1, finalist1posX+this.entryWidth, 0, posY, finalist1.attachNode.right, this.directions.right)
        + this.generateBracketLevel(roundsNo-1, finalist1posX+this.entryWidth, posY, drawRegionSize.height, finalist1.attachNode.right, this.directions.right);
    }
  
    generateBracketLevel(roundNo, posX, fromY, toY, parentNode, direction) {
      if (roundNo > 0) {
        var posY = fromY + (toY - fromY) / 2;
        var participantSvg = new ParticipantSVG(posX, posY, 'user', 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?f=y');
        var newPosX;
        var newParentNode;
        var brokenLine;
        if (direction == this.directions.left) {
          newPosX = posX - this.entryWidth;
          newParentNode = participantSvg.attachNode.left;
          brokenLine = new BrokenLine(parentNode, participantSvg.attachNode.right);
        } else {
          newPosX = posX + this.entryWidth;
          newParentNode = participantSvg.attachNode.right;
          brokenLine = new BrokenLine(participantSvg.attachNode.left, parentNode);
        }
        return participantSvg.html + brokenLine.html
          + this.generateBracketLevel(roundNo-1, newPosX, fromY, posY, newParentNode, direction)
          + this.generateBracketLevel(roundNo-1, newPosX, posY, toY, newParentNode, direction);
      } else {
        return "";
      }
    }
  }
