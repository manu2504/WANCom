-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema tec
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tec
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tec` DEFAULT CHARACTER SET utf8 ;
USE `tec` ;

-- -----------------------------------------------------
-- Table `tec`.`EndNodes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tec`.`EndNodes` (
  `idNode` INT NOT NULL AUTO_INCREMENT,
  `ip` VARCHAR(16) NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`idNode`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tec`.`TraceDirections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tec`.`TraceDirections` (
  `idTraceDirection` INT NOT NULL AUTO_INCREMENT,
  `idSrc` INT NOT NULL,
  `idDst` INT NOT NULL,
  PRIMARY KEY (`idTraceDirection`),
  INDEX `fk_ClassPaths_Nodes1_idx` (`idSrc` ASC),
  INDEX `fk_ClassPaths_Nodes2_idx` (`idDst` ASC),
  CONSTRAINT `fk_ClassPaths_Nodes1`
    FOREIGN KEY (`idSrc`)
    REFERENCES `tec`.`EndNodes` (`idNode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ClassPaths_Nodes2`
    FOREIGN KEY (`idDst`)
    REFERENCES `tec`.`EndNodes` (`idNode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tec`.`Paths`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tec`.`Paths` (
  `idPath` INT NOT NULL AUTO_INCREMENT,
  `idTraceDirection` INT NOT NULL,
  PRIMARY KEY (`idPath`),
  INDEX `fk_Paths_ClassPaths1_idx` (`idTraceDirection` ASC),
  CONSTRAINT `fk_Paths_ClassPaths1`
    FOREIGN KEY (`idTraceDirection`)
    REFERENCES `tec`.`TraceDirections` (`idTraceDirection`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tec`.`Hops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tec`.`Hops` (
  `idHop` INT NOT NULL AUTO_INCREMENT,
  `idPath` INT NOT NULL,
  `ipSrc` VARCHAR(15) NOT NULL,
  `ipDst` VARCHAR(15) NOT NULL,
  `idPredecessor` INT NULL,
  PRIMARY KEY (`idHop`),
  INDEX `fk_Hops_Hops1_idx` (`idPredecessor` ASC),
  INDEX `fk_Hops_Paths1_idx` (`idPath` ASC),
  CONSTRAINT `fk_Hops_Hops1`
    FOREIGN KEY (`idPredecessor`)
    REFERENCES `tec`.`Hops` (`idHop`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Hops_Paths1`
    FOREIGN KEY (`idPath`)
    REFERENCES `tec`.`Paths` (`idPath`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tec`.`Measurements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tec`.`Measurements` (
  `idMeasurement` INT NOT NULL AUTO_INCREMENT,
  `idPath` INT NOT NULL,
  `rtt_ns` BIGINT(16) NOT NULL,
  `owd_forward_ns` BIGINT(16) UNSIGNED NULL,
  `owd_reverse_ns` BIGINT(16) UNSIGNED NULL,
  `timestamp_ns` BIGINT(16) NULL,
  `pair` BIGINT(16) NULL,
  PRIMARY KEY (`idMeasurement`),
  INDEX `fk_Measurements_Paths1_idx` (`idPath` ASC),
  UNIQUE INDEX `timestamp_ns_UNIQUE` (`timestamp_ns` ASC),
  CONSTRAINT `fk_Measurements_Paths1`
    FOREIGN KEY (`idPath`)
    REFERENCES `tec`.`Paths` (`idPath`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tec`.`HopMeasurements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tec`.`HopMeasurements` (
  `idHopMeasurement` INT NOT NULL AUTO_INCREMENT,
  `ipSrc` VARCHAR(45) NOT NULL,
  `ipDst` VARCHAR(45) NOT NULL,
  `rtt_ns` BIGINT(16) NOT NULL,
  `measurementTimestamp` BIGINT(16) NOT NULL,
  PRIMARY KEY (`idHopMeasurement`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
