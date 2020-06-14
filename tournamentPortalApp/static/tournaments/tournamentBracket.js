class ParticipantSVG {
    constructor(centerPositionX, centerPositionY, matches, roundNo, pairNo, participantNo) {
      const boxWidth = 160;
      const boxHeight = 60;
      const positionX = centerPositionX - boxWidth/2;
      const positionY = centerPositionY - boxHeight/2;
      if (matches && matches[roundNo] && matches[roundNo][pairNo] && matches[roundNo][pairNo].participants[participantNo]) {
        const avatarSize = 40;
        const padding = 10;
        const avatarPositionX = positionX + padding;
        const avatarPositionY = positionY + padding;
        const firstNamePositionX = positionX + avatarSize + 2*padding;
        const firstNamePositionY = positionY + boxHeight/2 - padding/2;
        const lastNamePositionX = firstNamePositionX;
        const lastNamePositionY = firstNamePositionY + padding*2;
        const participant = matches[roundNo][pairNo].participants[participantNo]
        const firstName = participant.first_name;
        const lastName = participant.last_name;
        const avatarAddress = participant.gravatar;
        this.html = `<rect x="${positionX}" y="${positionY}" width="${boxWidth}" height="${boxHeight}" style="fill:none;stroke:#000000"/><text x="${firstNamePositionX}" y="${firstNamePositionY}" fill="#000000">${firstName}</text><text x="${lastNamePositionX}" y="${lastNamePositionY}" fill="#000000">${lastName}</text><image href="${avatarAddress}" height="${avatarSize}" width="${avatarSize}" x="${avatarPositionX}" y="${avatarPositionY}"/>`;
      } else {
        this.html = `<rect x="${positionX}" y="${positionY}" width="${boxWidth}" height="${boxHeight}" style="fill:none;stroke:#000000"/>`;
      }
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
    constructor(matches) {
      this.entryWidth = 180;
      this.entryHeight = 100;
      const roundsNo = matches.length;
      // Estimate size
      this.svgWidth = this.entryWidth * 2 * roundsNo;
      this.svgHeight = this.entryHeight*2 * 2^(roundsNo);
      const posX = this.svgWidth / 2;
      const posY = this.svgHeight / 2;
      var winner = new ParticipantSVG(posX, posY, matches, 0, 0, 0);
      var finalist0posX = posX - this.entryWidth;
      var finalist1posX = posX + this.entryWidth;
      var finalist0 = new ParticipantSVG(finalist0posX, posY, matches, 1, 0, 0);
      var finalist1 = new ParticipantSVG(finalist1posX, posY, matches, 1, 0, 1);

      this.svgHtml = winner.html + finalist0.html + finalist1.html
        + new BrokenLine(finalist0.attachNode.right, winner.attachNode.left).html
        + new BrokenLine(winner.attachNode.right, finalist1.attachNode.left).html
        + this.generateBracketLevel(matches, 2, 0, 0, roundsNo, finalist0posX-this.entryWidth, 0, posY, finalist0.attachNode.left, this.directions.left)
        + this.generateBracketLevel(matches, 2, 0, 1, roundsNo, finalist0posX-this.entryWidth, posY, this.svgHeight, finalist0.attachNode.left, this.directions.left)
        + this.generateBracketLevel(matches, 2, 1, 0, roundsNo, finalist1posX+this.entryWidth, 0, posY, finalist1.attachNode.right, this.directions.right)
        + this.generateBracketLevel(matches, 2, 1, 1, roundsNo, finalist1posX+this.entryWidth, posY, this.svgHeight, finalist1.attachNode.right, this.directions.right);
    }
  
    generateBracketLevel(matches, currentRoundNo, pairNo, participantNo, maxRoundNo, posX, fromY, toY, parentNode, direction) {
      if (currentRoundNo < maxRoundNo) {
        var posY = fromY + (toY - fromY) / 2;
        var participantSvg = new ParticipantSVG(posX, posY, matches, currentRoundNo, pairNo, participantNo);
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
        var nextPairNo = 2*pairNo + participantNo;
        return participantSvg.html + brokenLine.html
          + this.generateBracketLevel(matches, currentRoundNo+1, nextPairNo, 0, maxRoundNo, newPosX, fromY, posY, newParentNode, direction)
          + this.generateBracketLevel(matches, currentRoundNo+1, nextPairNo, 1, maxRoundNo, newPosX, posY, toY, newParentNode, direction);
      } else {
        return "";
      }
    }
  }
