import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Car } from './car.entity';
import { CarController } from './car.controller';
import { CarService } from './car.service';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'sqlite',
      database: 'cars.db',
      entities: [Car],
      synchronize: true,
    }),
    TypeOrmModule.forFeature([Car])],
  controllers: [CarController],
  providers: [CarService],
})
export class AppModule {}
